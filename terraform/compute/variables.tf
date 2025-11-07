variable "ecr_repository_url" {
  type        = string
  description = "Image URL for AWS Batch job"
}
variable "subnet_ids" {
  type        = list(string)
  description = "Subnet ID for AWS Batch job"
}
variable "security_group_ids" {
  type        = list(string)
  description = "Security group ID for AWS Batch job"
}
