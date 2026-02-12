variable "instance_type" {
  type = string
}

variable "key_name" {
  type = string
}

variable "security_group_ids" {
  type = list(string)
}

variable "instance_count" {
  type = number
}

variable "user_data" {
  type = string
}

variable "tags" {
  type = string
}
