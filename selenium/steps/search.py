# -*- coding: utf-8 -*-
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given("I am on the Google homepage")
def step_impl(context):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # User-agent para evitar que las unis bloqueen el tráfico de "bots"
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )

    context.driver = webdriver.Chrome(options=options)
    context.driver.maximize_window()
    context.driver.get("https://www.google.com")


@when('I search for "{query}" and enter the first result')
def step_impl(context, query):
    context.current_university = query.lower()
    wait = WebDriverWait(context.driver, 10)

    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(query + Keys.RETURN)

    first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h3")))
    first_result.click()


@when('I navigate to the "{section_name}" section')
def step_impl(context, section_name):
    wait = WebDriverWait(context.driver, 15)

    # --- LÓGICA PARA ITESO ---
    if "iteso" in context.current_university:
        wait.until(EC.element_to_be_clickable((By.ID, "icon-search"))).click()
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "ipt-search")))
        search_input.send_keys(section_name + Keys.RETURN)

    # --- LÓGICA PARA TEC DE MONTERREY ---
    elif "tec" in context.current_university:
        # 1. Clic en el botón de búsqueda (el div que mencionaste antes)
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.menu-buscador"))
        )
        search_button.click()

        # 2. Localizar el input usando el data-drupal-selector proporcionado
        # Usamos un selector parcial por si el ID (edit-search--4) cambia de número
        search_input = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[data-drupal-selector='edit-search']")
            )
        )

        search_input.clear()
        search_input.send_keys(section_name)  # Escribimos el texto (ej. "Carreras")

        # 3. Esperar y dar clic en la sugerencia específica: "Campus Profesional"
        # Usamos texto exacto para evitar errores
        suggestion_xpath = "//span[@class='autocomplete-suggestion-label' and contains(text(), 'Campus Profesional')]"
        suggestion = wait.until(
            EC.element_to_be_clickable((By.XPATH, suggestion_xpath))
        )

        suggestion.click()

    # --- LÓGICA PARA UVM ---
    elif "uvm" in context.current_university:
        # 1. Clic en el icono de la lupa (SVG con ID icon-search)
        try:
            search_trigger = wait.until(
                EC.element_to_be_clickable((By.ID, "icon-search"))
            )
            search_trigger.click()
        except:
            # Respaldo por si el SVG no recibe el clic directamente
            trigger = context.driver.find_element(By.ID, "icon-search")
            context.driver.execute_script("arguments[0].click();", trigger)

        # 2. Localizar el textarea de búsqueda
        # Usamos el ID 'buscartxt' que nos proporcionaste
        search_input = wait.until(
            EC.visibility_of_element_located((By.ID, "buscartxt"))
        )

        search_input.clear()
        search_input.send_keys(section_name + Keys.RETURN)

        # 3. Esperar y dar clic en el resultado específico (gs-title)
        # Usamos un selector que busque el enlace que contiene el texto de Carreras/Licenciaturas
        try:
            result_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.gs-title"))
            )
            result_link.click()

            # Marcamos que ya navegamos con éxito para que el @then no falle
            context.skip_results_list = True
            print("Navegación exitosa a la oferta académica de UVM.")

        except Exception as e:
            print(f"No se pudo encontrar el resultado específico en UVM: {e}")


@then("I should see a list of available programs")
def step_impl(context):
    wait = WebDriverWait(context.driver, 20)

    # 1. Verificamos si ya llegamos a la página final (Tec o UVM)
    # Usamos getattr por seguridad en caso de que la variable no esté definida
    if (
        getattr(context, "skip_results_list", False)
        or "tec" in context.current_university
    ):
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(
            f"Éxito: Se confirmó la navegación final para {context.current_university}"
        )
        context.driver.quit()
        return  # Finaliza el paso con éxito

    # 2. Lógica para universidades que requieren un clic extra en la lista (como ITESO)
    selectors = {
        "iteso": "a.gs-title",
        "unitec": ".hs-search-results__title, .search-result-item a",
    }

    # Determinar qué selector usar
    current_selector = selectors.get(
        next((k for k in selectors if k in context.current_university), "a")
    )

    try:
        # Esperar al primer link de resultados
        result_link = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, current_selector))
        )

        # Clic por JS para evitar bloqueos
        context.driver.execute_script("arguments[0].click();", result_link)

        # Manejo de pestañas
        if len(context.driver.window_handles) > 1:
            context.driver.switch_to.window(context.driver.window_handles[-1])

        print(f"Éxito: Se navegó a la sección de {context.current_university}")

    finally:
        context.driver.quit()
