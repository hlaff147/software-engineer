package user.userApi.exception

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.validation.FieldError
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler
import user.userApi.service.EmailAlreadyUsedException
import user.userApi.service.NotFoundException

@ControllerAdvice
class RestExceptionHandler {

    data class ErrorBody(val message: String, val details: Map<String, String>? = null)

    @ExceptionHandler(NotFoundException::class)
    fun handleNotFound(ex: NotFoundException): ResponseEntity<ErrorBody> =
        ResponseEntity.status(HttpStatus.NOT_FOUND).body(ErrorBody(ex.message ?: "Not found"))

    @ExceptionHandler(EmailAlreadyUsedException::class)
    fun handleConflict(ex: EmailAlreadyUsedException): ResponseEntity<ErrorBody> =
        ResponseEntity.status(HttpStatus.CONFLICT).body(ErrorBody(ex.message ?: "Conflict"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<ErrorBody> {
        val details = ex.bindingResult.allErrors
            .filterIsInstance<FieldError>()
            .associate { it.field to (it.defaultMessage ?: "invalid") }
        return ResponseEntity.badRequest().body(ErrorBody("Validation error", details))
    }
}
