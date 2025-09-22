variable "spotify_access_token" {
  type        = string
  description = "Spotify API access token"
  sensitive   = true
}

variable "playlist_name" {
  type        = string
  description = "Name of the playlist to create"
  default     = "My Terraform Playlist"
}

variable "playlist_description" {
  type        = string
  description = "Description of the playlist"
  default     = "Created automatically with Terraform HCL"
}

variable "playlist_public" {
  type        = bool
  description = "Whether the playlist is public or private"
  default     = false
}

variable "tracks" {
  description = "Map of track names and their Spotify IDs"
  type        = map(string)
}