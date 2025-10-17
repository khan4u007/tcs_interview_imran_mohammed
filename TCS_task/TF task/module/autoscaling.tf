resource "aws_autoscaling_group" "asg" {
  name                      = var.autoscaling_group_name
  desired_capacity          = 1
  max_size                  = 1
  min_size                  = 1
  vpc_zone_identifier       = var.private_subnet_ids
  health_check_type         = "EC2"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.lt.id
    version = "$Latest"
  }

  lifecycle {
    create_before_destroy = true
  }

  tag {
    key                 = "Name"
    value               = "${var.autoscaling_group_name}-instance"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_schedule" "rotate_instance" {
  scheduled_action_name  = "${var.autoscaling_group_name}-rotate"
  autoscaling_group_name = aws_autoscaling_group.asg.name
  recurrence             = "0 0 1 */1 *" # Every 1st of the month
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
}
