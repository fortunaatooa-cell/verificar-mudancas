terraform {
  required_version = "= 1.16.4"
}

variable "identifier" {
  type    = string
  default = "orders-prod"
}

variable "owner" {
  type    = string
  default = "team-a"
}

resource "terraform_data" "orders" {
  input = {
    owner = var.owner
  }

  triggers_replace = [var.identifier]
}

output "owner" {
  value = terraform_data.orders.output.owner
}
