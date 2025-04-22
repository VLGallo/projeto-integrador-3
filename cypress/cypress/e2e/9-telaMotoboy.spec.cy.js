describe("Teste de login", () => {
    before(() => {
      cy.visit(Cypress.config("baseUrl"));
      cy.get('[data-testid="login-input"]').type("AstDest");
      cy.get('[data-testid="senha-input"]').type("123");
      cy.get('[data-testid="entrar-btn"]').click();
      cy.saveSessionState();
    });

    it("Deve exibir modal de boas-vindas e cancelar pedido", () => {
        cy.get('[data-testid="motoboy-welcome-text"]').should("be.visible");
        cy.get('[data-testid="modal-ok-btn"]').click();
        cy.get('[data-testid="motoboy-welcome-text"]').should("not.exist");
        cy.get('[aria-label="cancelar-pedido-btn"]').click();

    });
  });