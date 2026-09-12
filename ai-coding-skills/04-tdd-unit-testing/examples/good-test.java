@Test
void should_ReturnProcessedOrder_When_ValidInputProvided() {
    // Arrange
    var input = OrderFixture.validOrder();
    when(repository.save(any())).thenReturn(input);

    // Act
    var result = service.process(input);

    // Assert
    assertThat(result).isNotNull();
    assertThat(result.status()).isEqualTo(Status.PROCESSED);
    verify(repository).save(any());
}

@Test
void should_ThrowValidationException_When_InputIsNull() {
    assertThatThrownBy(() -> service.process(null))
        .isInstanceOf(ValidationException.class)
        .hasMessageContaining("Input must not be null");
}
