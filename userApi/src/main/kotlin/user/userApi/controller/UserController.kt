package user.userApi.controller

import jakarta.validation.Valid
import org.springframework.data.domain.Page
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*
import user.userApi.dto.CreateUserRequest
import user.userApi.dto.UpdateUserRequest
import user.userApi.dto.UserResponse
import user.userApi.mapper.toResponse
import user.userApi.service.UserService

@RestController
@RequestMapping("/api/users")
class UserController(
    private val service: UserService
) {
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    fun create(@RequestBody @Valid req: CreateUserRequest): UserResponse =
        service.create(req).toResponse()

    @GetMapping("/{id}")
    fun get(@PathVariable id: String): UserResponse =
        service.get(id).toResponse()

    @GetMapping
    fun list(
        @RequestParam(defaultValue = "0") page: Int,
        @RequestParam(defaultValue = "10") size: Int
    ): Page<UserResponse> =
        service.list(page, size).map { it.toResponse() }

    @PatchMapping("/{id}")
    fun update(@PathVariable id: String, @RequestBody @Valid req: UpdateUserRequest): UserResponse =
        service.update(id, req).toResponse()

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    fun delete(@PathVariable id: String) {
        service.delete(id)
    }
}
