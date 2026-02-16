package br.com.corabank;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(
		classes = {corabank.CorabankApplication.class},
		webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT
)
public class CorabankApplicationTests {

	@Test
	public void contextLoads() {
	}

}
