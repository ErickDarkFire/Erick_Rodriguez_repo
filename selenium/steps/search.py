from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


@given("I am on the DuckDuckGo homepage")
def step_impl(context):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    context.driver = webdriver.Chrome(options=options)
    context.driver.get("https://duckduckgo.com")


@when('I search for "{query}" and enter the first result')
def step_impl(context, query):
    context.current_university = query.lower()
    wait = WebDriverWait(context.driver, 20)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys(query + Keys.RETURN)
    try:
        result_selector = "a[data-testid='result-title-a']"
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, result_selector)))
        results = context.driver.find_elements(By.CSS_SELECTOR, result_selector)
        first_result = results[0]

        context.driver.execute_script(
            "arguments[0].scrollIntoView(true);", first_result
        )
        context.driver.execute_script("arguments[0].click();", first_result)

    except Exception as e:
        file_path = "error_duck_dump.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(context.driver.page_source)
        print(
            f"DEBUG: No se encontró resultado en DuckDuckGo. HTML guardado en {os.path.abspath(file_path)}"
        )
        raise e


@when('I navigate to the "{section_name}" section')
def step_impl(context, section_name):
    wait = WebDriverWait(context.driver, 20)

    if "iteso" in context.current_university:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        try:
            search_trigger = wait.until(
                EC.presence_of_element_located((By.ID, "icon-search"))
            )
            context.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", search_trigger
            )
            context.driver.execute_script("arguments[0].click();", search_trigger)
            print("DEBUG: Se envió clic forzado al icono de búsqueda.")

        except Exception as e:
            print("DEBUG: Falló clic en icono, intentando con el contenedor LI...")
            li_trigger = context.driver.find_element(
                By.CSS_SELECTOR, "li#layout .searchmenu"
            )
            context.driver.execute_script("arguments[0].click();", li_trigger)
        search_input = wait.until(
            EC.visibility_of_element_located((By.ID, "ipt-search"))
        )
        search_input.clear()
        search_input.send_keys(section_name + Keys.RETURN)

    elif "tec" in context.current_university:
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.menu-buscador"))
        )
        search_button.click()
        search_input = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[data-drupal-selector='edit-search']")
            )
        )
        search_input.clear()
        search_input.send_keys(section_name)
        suggestion = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[@class='autocomplete-suggestion-label' and contains(text(), 'Campus Profesional')]",
                )
            )
        )
        suggestion.click()

    # --- LÓGICA PARA CUCBA ---
    elif "cucba" in context.current_university:
        # 1. Espera de carga y scroll al inicio
        wait = WebDriverWait(context.driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        context.driver.execute_script("window.scrollTo(0, 0);")

        try:
            # 2. Localizar el input por ID (Drupal suele usar edit-search-block-form--2)
            # Usamos un selector CSS que soporte el ID exacto que proporcionaste
            search_input = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input#edit-search-block-form--2")
                )
            )

            # 3. Limpiar y escribir con un pequeño delay para asegurar el foco
            search_input.clear()
            search_input.click()
            search_input.send_keys(section_name + Keys.RETURN)
            print(f"DEBUG: Búsqueda '{section_name}' enviada correctamente en CUCBA.")

        except Exception as e:
            print(f"DEBUG: Selector de ID falló en CUCBA, intentando por nombre...")
            # Plan B: Buscar por el atributo name que es search_block_form
            search_input = context.driver.find_element(By.NAME, "search_block_form")
            context.driver.execute_script("arguments[0].value = '';", search_input)
            search_input.send_keys(section_name + Keys.RETURN)


@then("I should see a list of available programs")
def step_impl(context):
    wait = WebDriverWait(context.driver, 30)

    # 1. Definir selectores (Aseguramos CUCBA)
    selectors = {
        "iteso": "a.gs-title",
        "unitec": "a.hs-search-results__title",
        "cucba": "div.view-content a, div.search-results a, h3.title a",
    }

    current_selector = None
    for key in selectors:
        if key in context.current_university.lower():
            current_selector = selectors[key]
            break

    if not current_selector:
        current_selector = "a"

    # 2. Bucle de re-intento para manejar StaleElementReference
    attempts = 0
    while attempts < 3:
        try:
            # Volvemos a buscar el elemento en cada intento
            result_link = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, current_selector))
            )

            # Forzamos scroll y clic por JS
            context.driver.execute_script(
                "arguments[0].scrollIntoView(true);", result_link
            )
            context.driver.execute_script("arguments[0].click();", result_link)

            print(
                f"Éxito: Clic realizado en el resultado de {context.current_university}"
            )
            break  # Salimos del bucle si el clic funciona

        except StaleElementReferenceException:
            attempts += 1
            print(
                f"DEBUG: Elemento obsoleto (stale), reintentando búsqueda... ({attempts}/3)"
            )
            import time

            time.sleep(1)  # Pausa mínima para que el DOM se asiente

        except Exception as e:
            print(f"DEBUG: Error inesperado en el paso final: {e}")
            context.driver.save_screenshot("final_error_debug.png")
            raise e

    # Cerramos sesión después de una breve espera para ver la carga final
    import time

    time.sleep(2)
    context.driver.quit()
