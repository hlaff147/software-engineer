package user.userApi.dto

import jakarta.validation.constraints.Email
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size

data class CreateUserRequest(
    @field:NotBlank @field:Size(min = 2, max = 120)
    val name: String,
    @field:NotBlank @field:Email
    val email: String,
    @field:NotBlank @field:Size(min = 6, max = 72)
    val password: String
)

data class UpdateUserRequest(
    @field:Size(min = 2, max = 120)
    val name: String? = null,
    val active: Boolean? = null,
    @field:Size(min = 6, max = 72)
    val newPassword: String? = null
)

data class UserResponse(
    val id: String,
    val name: String,
    val email: String,
    val active: Boolean
)
