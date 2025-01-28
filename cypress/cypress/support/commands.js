// Salva o estado da sessão (localStorage, cookies e sessionStorage)
Cypress.Commands.add('saveSessionState', () => {
  console.log("Salvando o estado da sessão");
  const localStorageState = {...localStorage}; 
  const sessionStorageState = {...sessionStorage};
  const cookiesState = document.cookie;

  // Armazena o estado da sessão em objetos globais
  window.localStorageState = localStorageState;
  window.sessionStorageState = sessionStorageState;
  window.cookiesState = cookiesState;
});

// Restaura o estado da sessão (localStorage, cookies e sessionStorage)
Cypress.Commands.add('restoreSessionState', () => {
  // Restaura o localStorage
  if (window.localStorageState) {
    Object.keys(window.localStorageState).forEach((key) => {
      localStorage.setItem(key, window.localStorageState[key]);
    });
  }
  // Restaura o sessionStorage
  if (window.sessionStorageState) {
    Object.keys(window.sessionStorageState).forEach((key) => {
      sessionStorage.setItem(key, window.sessionStorageState[key]);
    });
  }
  // Restaura os cookies
  if (window.cookiesState) {
    document.cookie = window.cookiesState;
  }
});
