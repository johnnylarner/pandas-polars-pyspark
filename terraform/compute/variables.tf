variable "ecr_repository_url" {
  type        = string
  description = "Image URL for AWS Batch job"
}
variable "subnet_id" {
  type        = string
  description = "Subnet ID for AWS Batch job"
}
variable "security_group_id" {
  type        = string
  description = "Security group ID for AWS Batch job"
}
