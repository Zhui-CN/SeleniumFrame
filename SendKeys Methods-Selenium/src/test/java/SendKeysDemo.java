import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;

import java.io.IOException;

public class SendKeysDemo extends  Browser{

    @Test
    public void Check() throws IOException {

        driver = initializeDriver();
        driver.get("https://www.youtube.com/");
        driver.findElement(By.xpath("//input[@id='search']")).click();
        driver.findElement(By.xpath("//input[@id='search']")).sendKeys("Selenium");
        driver.findElement(By.xpath("//input[@id='search']")).sendKeys(Keys.ENTER);
    }
}
