START_PWD=$PWD
echo "Sourcing ROS workspace: $1"
cd $1
. /opt/ros/kinetic/setup.bash
. devel/setup.sh
cd $START_PWD