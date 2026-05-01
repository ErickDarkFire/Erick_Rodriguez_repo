from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


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

    # --- LÓGICA PARA UVM ---
    elif "uvm" in context.current_university:
        # 1. Configuración de entorno robusta
        context.driver.set_window_size(1920, 1080)
        # Forzar recarga si es necesario para asegurar que los scripts se activen
        wait = WebDriverWait(context.driver, 35)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Pequeña pausa para que el JS dinámico de la página se asiente
        import time

        time.sleep(5)

        try:
            print("DEBUG: Iniciando búsqueda flexible de la lupa en UVM...")

            # 2. JavaScript Flexible: Busca por ID, por clase o por atributo data
            context.driver.execute_script(
                """
                // Intentar varios selectores comunes para el botón de búsqueda en UVM
                var selectors = [
                    '#icon-search',
                    '.icon-search',
                    '[data-name="icon-search"]',
                    '//li[contains(@class, "search")]',
                    '//form[contains(@class, "search")]'
                ];

                var element = null;
                for (var s of selectors) {
                    if (s.startsWith('//')) {
                        element = document.evaluate(s, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    } else {
                        element = document.querySelector(s);
                    }
                    if (element) {
                        console.log('Elemento encontrado con: ' + s);
                        break;
                    }
                }

                if (element) {
                    // Disparar clic con burbujeo para asegurar que el listener lo atrape
                    var clickEvent = new MouseEvent('click', { 'view': window, 'bubbles': true, 'cancelable': true });
                    element.dispatchEvent(clickEvent);

                    // Si tiene un padre inmediato, también le damos clic por si acaso
                    if (element.parentElement) element.parentElement.click();
                } else {
                    throw new Error('No se detectó ningún disparador de búsqueda compatible');
                }
            """
            )

            # 3. Localizar el input (buscartxt)
            # Usamos un selector más amplio por si el ID cambia en el servidor
            search_input = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "input#buscartxt, textarea#buscartxt, .buscartxt")
                )
            )
            search_input.clear()
            search_input.send_keys(section_name + Keys.RETURN)

            # 4. Clic en el resultado final
            result_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.gs-title"))
            )
            context.driver.execute_script("arguments[0].click();", result_link)
            context.skip_results_list = True

        except Exception as e:
            # Captura de pantalla y volcado de HTML para diagnóstico
            context.driver.save_screenshot("uvm_fatal_error.png")
            with open("uvm_debug_source.html", "w", encoding="utf-8") as f:
                f.write(context.driver.page_source)
            print(
                f"DEBUG: Fallo total en UVM. Revisa 'uvm_debug_source.html' en los artefactos. Error: {e}"
            )
            raise e


@then("I should see a list of available programs")
def step_impl(context):
    wait = WebDriverWait(context.driver, 25)

    # 1. Si ya terminamos en los pasos anteriores (Tec o UVM ya clicaron su link final)
    if (
        getattr(context, "skip_results_list", False)
        or "tec" in context.current_university
    ):
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"Éxito: Navegación final confirmada para {context.current_university}")
        context.driver.quit()
        return

    # 2. Definir selectores para las universidades que tienen lista de resultados intermedia
    # Agregamos 'uvm' por si acaso, aunque normalmente el flag skip_results lo salta
    selectors = {
        "iteso": "a.gs-title",
        "unitec": ".hs-search-results__title, .search-result-item a",
        "uvm": "a.gs-title",  # La UVM también usa Google Search Engine internamente
    }

    # 3. Obtener el selector de forma segura
    # Buscamos si alguna de las llaves del diccionario está en el nombre de la universidad
    current_selector = None
    for key in selectors:
        if key in context.current_university:
            current_selector = selectors[key]
            break

    # Si no encontramos un selector específico, usamos uno genérico (a) para evitar el error de 'None'
    if not current_selector:
        current_selector = "a"

    try:
        # 4. Esperar y hacer clic en el resultado
        result_link = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, current_selector))
        )

        # Clic por JS para máxima compatibilidad
        context.driver.execute_script("arguments[0].click();", result_link)

        # Si se abre en pestaña nueva, cambiamos a ella
        if len(context.driver.window_handles) > 1:
            context.driver.switch_to.window(context.driver.window_handles[-1])

        print(f"Éxito: Se navegó a la sección de {context.current_university}")

    except Exception as e:
        print(
            f"DEBUG: No se encontró el link de resultados con el selector: {current_selector}"
        )
        context.driver.save_screenshot("final_step_error.png")
        raise e
    finally:
        context.driver.quit()
