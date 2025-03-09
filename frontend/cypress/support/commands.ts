// ***********************************************
// This file contains custom Cypress commands
// ***********************************************

// -- This is a parent command --
Cypress.Commands.add('login', (username: string, password: string) => {
  // Login implementation (if/when needed)
});

// -- This is a child command --
Cypress.Commands.add('findByTestId', { prevSubject: 'element' }, (subject, testId) => {
  return subject.find(`[data-testid=${testId}]`);
});

// -- This is a dual command --
Cypress.Commands.add('getByTestId', (testId) => {
  return cy.get(`[data-testid=${testId}]`);
});

// -- Type declarations for custom commands --
declare global {
  namespace Cypress {
    interface Chainable {
      login(username: string, password: string): Chainable<void>;
      findByTestId(testId: string): Chainable<JQuery<HTMLElement>>;
      getByTestId(testId: string): Chainable<JQuery<HTMLElement>>;
    }
  }
}