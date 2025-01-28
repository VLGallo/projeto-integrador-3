describe("Atribuição de Pedido", () => {
  before(() => {
    cy.visit(Cypress.config("baseUrl"));
    cy.get('[data-testid="login-input"]').type("vlgallo");
    cy.get('[data-testid="senha-input"]').type("123");
    cy.get('[data-testid="entrar-btn"]').click();
    cy.wait(3000);
    cy.saveSessionState();
  });

  it("Deve atribuir um novo pedido a um motoboy", () => {
    cy.get('[data-testid="atribuicao-btn"]').click();

    cy.wait(6000);

    cy.get("[data-testid='motoboy-picker']")
      .should("be.visible")
      .and("not.be.disabled");

 
    cy.get("[data-testid='motoboy-picker'] option")
      .should("have.length.greaterThan", 1); 

    cy.get("[data-testid='motoboy-picker']").select("Pedro de Oliveira Antunes");


    cy.get(".MuiListItemButton-root")
      .should("be.visible")
      .last()
      .find('input[type="checkbox"]')
      .should("exist")
      .and("not.be.disabled")
      .click();

    cy.get("[data-testid='adicionar-um-btn']")
      .should("be.visible")
      .and("not.be.disabled")
      .click();

    cy.get("[data-testid='atribuir-btn']")
      .should("be.visible")
      .and("not.be.disabled")
      .click();


    cy.contains("Pedido(s) atribuído(s) com sucesso").should("be.visible");
    //cy.get("body").type("{esc}");
  });
});
