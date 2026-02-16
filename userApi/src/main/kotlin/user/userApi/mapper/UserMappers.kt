package user.userApi.mapper

import user.userApi.domain.User
import user.userApi.dto.UserResponse

fun User.toResponse() = UserResponse(
    id = requireNotNull(id),
    name = name,
    email = email,
    active = active
)