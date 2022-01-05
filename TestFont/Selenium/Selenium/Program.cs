using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using OpenQA.Selenium;  
using OpenQA.Selenium.Chrome;

namespace Selenium
{
    class Program
    {
        static void Main(string[] args)
        {   
            IWebDriver driver = new ChromeDriver();

            try
            {
                driver.Navigate().GoToUrl("http://localhost:53997/");
                Thread.Sleep(2000);
                Console.Write("test login started ");

                Console.WriteLine("test login button ");

                IWebElement ele = driver.FindElement(By.Name("login"));
                ele.Click();

                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test login button success ");
                Console.ResetColor();
                Thread.Sleep(3000);

                ele = driver.FindElement(By.Name("email"));
                Console.WriteLine("test email textbox ");

                ele.SendKeys("popamorena3@gmail.com");
                  Thread.Sleep(2000);
                 ele.SendKeys(Keys.Enter);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test email textbox success ");

                Console.ResetColor();
                Console.WriteLine("test password textbox ");
                ele = driver.FindElement(By.Name("password"));
                ele.SendKeys("kid");
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test password textbox success ");

                Console.ResetColor();
                Console.WriteLine("test login button ");
                ele = driver.FindElement(By.Name("login"));
                 ele.Click();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test login button success ");
                Console.ForegroundColor = ConsoleColor.Green;
                ele = driver.FindElement(By.Name("superlike"));
                Console.WriteLine(" all tests success ");
                Console.ResetColor();
                Thread.Sleep(3000);
               
            }
            catch
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("test faild ");
                Console.ResetColor();
                Thread.Sleep(3000);

            }

            try
            {
                driver.Navigate().GoToUrl("http://localhost:53997/");
                Thread.Sleep(2000);
                Console.WriteLine("test sing-up started ");

                Console.WriteLine("test sing-up button ");

                IWebElement ele = driver.FindElement(By.Name("sing"));
                ele.Click();

                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test login button success ");
                Console.ResetColor();
                Thread.Sleep(3000);

                ele = driver.FindElement(By.Name("email"));
                Console.WriteLine("test email textbox ");
                ele.SendKeys("popamorena@gmail.com");
                Thread.Sleep(2000);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test email textbox success ");
                Console.ResetColor();

                Console.WriteLine("test password textbox ");
                ele = driver.FindElement(By.Name("password"));
                ele.SendKeys("kid");
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test password textbox success ");
                Console.ResetColor();

                Console.WriteLine("test conf_password textbox ");
                ele = driver.FindElement(By.Name("conf_password"));
                ele.SendKeys("kid");
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test conf_password textbox success ");
                Console.ResetColor();

                Console.WriteLine("test sign Up button ");
                ele = driver.FindElement(By.Name("submit"));
                ele.Click();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("test sign Up button success ");

                driver.Close();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine(" all tests success ");
                Console.ResetColor();
            }
            catch
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("test faild ");
                Console.ResetColor();

            }

            driver.Close();

        }
    }
}
