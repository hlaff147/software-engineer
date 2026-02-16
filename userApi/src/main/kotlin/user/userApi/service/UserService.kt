package user.userApi.service

import org.springframework.data.domain.Page
import org.springframework.data.domain.PageRequest
import org.springframework.security.crypto.bcrypt.BCrypt
import org.springframework.stereotype.Service
import user.userApi.domain.User
import user.userApi.dto.CreateUserRequest
import user.userApi.dto.UpdateUserRequest
import user.userApi.repository.UserRepository
import java.time.Instant

@Service
class UserService(
    private val repo: UserRepository
) {
    fun create(req: CreateUserRequest): User {
        if (repo.existsByEmail(req.email)) {
            throw EmailAlreadyUsedException(req.email)
        }
        val hash = BCrypt.hashpw(req.password, BCrypt.gensalt())
        val now = Instant.now()
        val user = User(
            email = req.email.trim(),
            name = req.name.trim(),
            passwordHash = hash,
            createdAt = now,
            updatedAt = now,
            active = true
        )
        return repo.save(user)
    }

    fun get(id: String): User =
        repo.findById(id).orElseThrow { NotFoundException("User $id not found") }

    fun list(page: Int, size: Int): Page<User> =
        repo.findAll(PageRequest.of(page.coerceAtLeast(0), size.coerceIn(1, 100)))

    fun update(id: String, req: UpdateUserRequest): User {
        val current = get(id)
        val updated = current.copy(
            name = req.name?.trim() ?: current.name,
            active = req.active ?: current.active,
            passwordHash = req.newPassword?.let { BCrypt.hashpw(it, BCrypt.gensalt()) } ?: current.passwordHash,
            updatedAt = Instant.now()
        )
        return repo.save(updated)
    }

    fun delete(id: String) {
        val u = get(id)
        repo.delete(u)
    }
}

class NotFoundException(message: String) : RuntimeException(message)
class EmailAlreadyUsedException(email: String) : RuntimeException("Email already in use: $email")
