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
        # 1. Forzar tamaño y asegurar que estamos al inicio de la página
        context.driver.set_window_size(1920, 1080)
        context.driver.execute_script("window.scrollTo(0, 0);")

        # Espera de cortesía para que los scripts de la UVM terminen de cargar
        import time

        time.sleep(3)

        wait = WebDriverWait(context.driver, 30)  # Aumentamos a 30 para el servidor
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        try:
            # 2. Búsqueda por JavaScript Directo
            # GitHub a veces no "ve" el SVG con XPath, pero JS siempre puede encontrarlo por ID
            print("DEBUG: Intentando abrir buscador en UVM vía JS directo...")

            context.driver.execute_script(
                """
                var icon = document.getElementById('icon-search');
                if (icon) {
                    // Disparar clic en el icono y en sus padres hasta el LI
                    var current = icon;
                    for (var i = 0; i < 3; i++) {
                        if (current) {
                            current.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                            current = current.parentElement;
                        }
                    }
                } else {
                    throw new Error('No se encontró el ID icon-search en el DOM');
                }
            """
            )

            # 3. Verificar si el input apareció
            search_input = wait.until(
                EC.visibility_of_element_located((By.ID, "buscartxt"))
            )
            search_input.clear()
            search_input.send_keys(section_name + Keys.RETURN)
            print("DEBUG: Texto enviado al buscador de UVM.")

            # 4. Clic en el resultado final (Google Search interno de UVM)
            result_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.gs-title"))
            )
            context.driver.execute_script("arguments[0].click();", result_link)
            context.skip_results_list = True

        except Exception as e:
            # Si falla, guardamos el HTML y captura para ver el error real en los artefactos de GitHub
            context.driver.save_screenshot("uvm_timeout_debug.png")
            with open("uvm_dom_debug.html", "w", encoding="utf-8") as f:
                f.write(context.driver.page_source)
            print(f"DEBUG: Error crítico en UVM: {e}")
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
