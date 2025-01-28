describe("Cadastro de Pedido", () => {
  before(() => {
    cy.visit(Cypress.config("baseUrl"));
    cy.get('[data-testid="login-input"]').type("vlgallo");
    cy.get('[data-testid="senha-input"]').type("123");
    cy.get('[data-testid="entrar-btn"]').click();
    cy.wait(3000);
    cy.saveSessionState();
  });

  it("Deve cadastrar um novo pedido", () => {
  
    cy.get('[data-testid="pedido-btn"]').click();

 
    cy.get("[data-testid='cliente-picker']").each(($select) => {
      cy.wrap($select)
        .find("option")
        .contains("Adelina de Oliveira Santos")
        .then(($option) => {
          cy.wrap($select).select($option.val());
        });
    });

    cy.get("[data-testid='list-item-117']").click();
    cy.get("[data-testid='list-item-96']").click(); 
    
    cy.get("[data-testid='move-selected-right-btn']").click();
    cy.get('[data-testid="salvar-btn"]').click();
    cy.contains("Pedido cadastrado com sucesso").should("be.visible");
    //cy.get("body").type("{esc}");
  });
});
