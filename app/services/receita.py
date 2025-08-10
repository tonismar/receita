from settings import Settings
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

settings = Settings()

class Receita:
    def __init__(self, cpf: str, nasc: str):
        self.cpf = cpf
        self.nasc = nasc

    async def check_cpf(self):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            ctx = await browser.new_context()
            page = await ctx.new_page()

            try:
                await page.goto(settings.url_cpf)
                
                # fill CPF
                await page.fill('input[name="txtCPF"]', str(self.cpf))
                # fill Data de Nascimento
                await page.fill('input[name="txtDataNascimento"]', str(self.nasc))

                # get and change to iframe from hCaptcha
                frame = page.frame_locator('iframe[title="Widget contendo caixa de seleção para desafio de segurança hCaptcha"]')

                # wait checkbox show and click
                await frame.locator('#checkbox').wait_for(timeout=10000)
                await frame.locator('#checkbox').click()

                # pause to wait captcha process
                await asyncio.sleep(3)

                # Enviar button click
                await page.click('input[name="Enviar"]')

                # wait load the result
                await page.wait_for_selector('.clConteudoDados')

                data_result = []
                data_content = await page.locator('.clConteudoDados').all_text_contents()
                data_result.extend([d.strip() for d in data_content])

                data_comp = await page.locator('.clConteudoComp').all_text_contents()
                data_result.extend([d.strip() for d in data_comp])

                # remove last 3 itens from array
                data_result = data_result[:-3]

                dict = {}
                for item in data_result:
                    if ": " in item:
                        key, val = item.split(": ", 1)
                        dict[key] = val

                return dict
            except Exception as e:
                raise RuntimeError(f"Error to query: {e}")
            finally:
                await browser.close()

