# SCALEWAY
variable "scaleway_access_key" {
  description = "Scaleway Access Key"
  type        = string
}
variable "scaleway_secret_key" {
  description = "Scaleway Secret Key"
  type        = string
  sensitive   = true
}
variable "scaleway_organization_id" {
  description = "Scaleway Organization ID"
  type        = string
}
variable "scaleway_project_id" {
  description = "Scaleway Project ID"
  type        = string
}
variable "scaleway_zone" {
  description = "Scaleway zone"
  type        = string
}
variable "scaleway_instance_type" {
  description = "Scaleway Instance Type"
  type        = string
  default     = "DEV1-M" # 2 vCPUs, 4GB RAM
}
variable "scaleway_instance_size" {
  description = "Scaleway Instance storage size in GB"
  type        = number
  default     = 40
}
variable "scaleway_server_user" {
  description = "Username for deployment"
  type        = string
}
variable "scaleway_ssh_pub_key_name" {
  description = "SSH pub key name"
  type        = string
}
variable "scaleway_ssh_private_key" {
  description = "Content of the private SSH key"
  type        = string
}

# DATA
variable "data_bucket" {
  description = "Scaleway bucket where the data is stored"
  type        = string
}
variable "data_source_key" {
  description = "Data filepath in bucket"
  type        = string
}

# INSTANCE
variable "wzrd_domain" {
  description = "(Sub)Domain where to deploy the app and get a certificate for"
  type        = string
}
variable "wzrd_github_token" {
  description = "GitHub PAT token dedicated to this repo"
  type        = string
}
variable "github_repo_name" {
  description = "GitHub repository"
  type        = string
}
variable "github_repo_branch" {
  description = "Branch to use with this GitHub repository"
  type        = string
}
variable "github_workspace" {
  description = "GitHub Actions workspace"
  type        = string
}

# APP
variable "anthropic_api_key" {
  description = "Anthropic API key"
  type        = string
}
