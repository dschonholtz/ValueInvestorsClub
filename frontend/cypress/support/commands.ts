// ***********************************************
// This file contains custom Cypress commands
// ***********************************************

// -- This is a parent command --
// eslint-disable-next-line @typescript-eslint/no-unused-vars
Cypress.Commands.add('login', (_username: string, _password: string) => {
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
// Using interface merging instead of namespace
declare global {
  interface Cypress {
    Chainable: {
      login(username: string, password: string): Cypress.Chainable<void>;
      findByTestId(testId: string): Cypress.Chainable<JQuery<HTMLElement>>;
      getByTestId(testId: string): Cypress.Chainable<JQuery<HTMLElement>>;
    }
  }
}