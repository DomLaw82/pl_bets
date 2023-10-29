variable "access_key" {
  type = string
  description = "Access key id to access AWS resources"
}

variable "secret_key" {
  type = string
  description = "Secret key to access AWS resources"
}

variable "region" {
  type = string
  description = "Secret key to access AWS resources"
  default = "eu-west-2"
}

variable "db_username" {
  type = string
}
variable "db_password" {
  type = string
}