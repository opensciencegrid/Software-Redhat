#!/bin/bash

DOCKER_ARGS=()
USER=1000
ENV_FILE=/etc/osg/ospool-ep.cfg
EP_IMG=release
# explicitly true:
# y(es), t(rue), 1, on; uppercase or lowercase
is_true () {
    case "${1^^}" in         # bash-ism to uppercase the var
        Y|YES) return 0 ;;
        T|TRUE) return 0 ;;
        ON) return 0 ;;
        1) return 0 ;;
    esac
    return 1
}

add_docker_arg() {
  DOCKER_ARGS+=("$@")
}

exit_with_error () {
  echo "Error: $1"
  exit 1
}

# Check that required parameters are non-empty
REQUIRED_ENV_VARS=(GLIDEIN_Site GLIDEIN_ResourceName ACCEPT_JOBS_FOR_HOURS RETIREMENT_HOURS)
for var in "${REQUIRED_ENV_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    exit_with_error "Required environment variable $var not set."
  fi
done

# Verify that TOKEN_LOCATION is set and a file
if [ -n "$TOKEN_LOCATION" ] && test -f "$TOKEN_LOCATION"; then
  add_docker_arg -v "${TOKEN_LOCATION}:/etc/condor/tokens-orig.d/flock.opensciencegrid.org"
else
  exit_with_error "TOKEN_LOCATION must be a file"
fi

# Verify that WORKER_TEMP_DIR is either a directory or is unset
if [ -n "$WORKER_TEMP_DIR" ] && ! test -d "$WORKER_TEMP_DIR"; then
  exit_with_error "WORKER_TEMP_DIR must be empty or a directory"
fi

if [ -n "$WORKER_TEMP_DIR" ] && test -d "$WORKER_TEMP_DIR"; then
  add_docker_arg -v "${WORKER_TEMP_DIR}:/pilot"
fi

# Verify that only one of BIND_MOUNT_CVMFS and CVMFSEXEC_REPOS is set
if is_true "$BIND_MOUNT_CVMFS" && [ -n "$CVMFSEXEC_REPOS" ]; then
  exit_with_error "Only one of BIND_MOUNT_CVMFS and CVMFSEXEC_REPOS should be set"
fi

if is_true "$BIND_MOUNT_CVMFS"; then
  add_docker_arg -v "/cvmfs:/cvmfs:shared"
fi

# Mount /etc/OpenCl/vendors if providing NVIDIA GPU resources,
# and use the cuda_11_8_0-release flavor of the ospool-ep img
if is_true "$PROVIDE_NVIDIA_GPU"; then
  add_docker_arg -v "/etc/OpenCL/vendors:/etc/OpenCL/vendors:ro"
  # Testing indicates that singularity PID namespaces conflict with GPU mount requirements
  add_docker_arg -e SINGULARITY_DISABLE_PID_NAMESPACES=True
  add_docker_arg --runtime nvidia
  EP_IMG=cuda_11_8_0-release
fi

# Limit docker's CPU usage if the NUM_CPUS condor config param is set
if [ -n "$NUM_CPUS" ]; then
  add_docker_arg "--cpus=$NUM_CPUS"
fi

# Limit docker's memory usage if the MEMORY condor config param is set
if [ -n "$MEMORY" ]; then
  add_docker_arg "--memory=$(( ($MEMORY + 100) * 1024 * 1024 ))"
fi

# TODO passing the whole source env file into docker pollutes the environment to some extent
docker run --user $USER --name ospool-ep-container \
    --security-opt seccomp=unconfined        \
    --security-opt systempaths=unconfined    \
    --security-opt no-new-privileges         \
    --device /dev/fuse                       \
    --pull=always            \
    --ulimit nofile=2048:2048 \
    --pids-limit=16384 \
    --env-file $ENV_FILE \
    "${DOCKER_ARGS[@]}" \
    hub.opensciencegrid.org/osg-htc/ospool-ep:%{OSGVER}-$EP_IMG
