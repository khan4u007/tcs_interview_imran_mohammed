module "ephemeral" {
  source                  = "./module"

  autoscaling_group_name = ""
  vpc_id                 = ""
  private_subnet_ids     = [""]

  certificate_arn        = ""
  load_balancer_url      = ""
}
