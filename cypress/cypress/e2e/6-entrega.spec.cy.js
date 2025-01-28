describe("Entrega de Pedido", () => {
  it("Deve entregar um novo pedido", () => {
    cy.visit("https://vlgallo.github.io/projeto-integrador-2/motoboy-page/index.html?motoboy=32");
    cy.wait(9500);
     cy.get('label').contains("Entregar").click();
    
    cy.get("#status-entrega").should("be.visible").and("contain", "Entregue");
  });
});
