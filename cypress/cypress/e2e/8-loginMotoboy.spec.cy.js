describe("Teste de login", () => {
  before(() => {
    cy.visit(Cypress.config("baseUrl"));
    cy.get('[data-testid="login-input"]').type("AstDest");
    cy.get('[data-testid="senha-input"]').type("123");
    cy.get('[data-testid="entrar-btn"]').click();
    cy.saveSessionState();
  });

  it("Deve estar logado", () => {
    cy.contains("Gestão de Entregas").should("be.visible");
  });
});
