describe("Cadastro de Motoboy", () => {
  before(() => {
    cy.visit(Cypress.config("baseUrl"));
    cy.get('[data-testid="login-input"]').type("vlgallo");
    cy.get('[data-testid="senha-input"]').type("123");
    cy.get('[data-testid="entrar-btn"]').click();
    cy.wait(3000)
    cy.saveSessionState();
  });

  it("Deve cadastrar um novo motoboy", () => {
    cy.get('[data-testid="cadastro-btn"]').click();
    cy.get('[data-testid="nome-entregador-input"]').type("Pedro de Oliveira Antunes");
    cy.get('[data-testid="telefone-entregador-input"]').type("16998774111");
    cy.get('[data-testid="placa-entregador-input"]').type("JAV1487");
    cy.get('[data-testid="salvar-entregador-btn"]').click();
    cy.contains("Entregador(a) cadastrado(a) com sucesso").should("be.visible");
    cy.get("body").type("{esc}");
  });
});
