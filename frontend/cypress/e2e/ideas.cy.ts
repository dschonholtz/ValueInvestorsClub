/**
 * End-to-end tests for the Ideas page
 */
describe('Ideas Page', () => {
  beforeEach(() => {
    // Visit the ideas page before each test
    cy.visit('/ideas');
    
    // Wait for page to load (should see a heading)
    cy.contains('Investment Ideas', { timeout: 10000 }).should('be.visible');
  });

  it('displays ideas from the API', () => {
    // Check that ideas are loaded and displayed
    cy.get('[data-testid="idea-card"]').should('have.length.at.least', 1);
  });

  it('filters ideas by company search', () => {
    // Enter company search term
    cy.get('[data-testid="company-search"]').type('Apple');
    
    // Wait for search results
    cy.get('[data-testid="company-option"]').contains('Apple').click();
    
    // Verify filtered results
    cy.url().should('include', 'company_id=');
  });

  it('filters ideas by user search', () => {
    // Enter user search term
    cy.get('[data-testid="user-search"]').type('test');
    
    // Wait for search results
    cy.get('[data-testid="user-option"]').first().click();
    
    // Verify filtered results
    cy.url().should('include', 'user_id=');
  });

  it('toggles between long and short ideas', () => {
    // Toggle to show only short ideas
    cy.get('[data-testid="short-ideas-toggle"]').click();
    
    // Verify URL parameter
    cy.url().should('include', 'is_short=true');
    
    // Toggle back to all ideas
    cy.get('[data-testid="short-ideas-toggle"]').click();
    
    // Verify parameter is removed
    cy.url().should('not.include', 'is_short=true');
  });

  it('loads more ideas when scrolling', () => {
    // Count initial ideas
    cy.get('[data-testid="idea-card"]').then($initialCards => {
      const initialCount = $initialCards.length;
      
      // Scroll to the bottom to trigger loading more
      cy.get('[data-testid="load-more-button"]').scrollIntoView().click();
      
      // Verify more ideas are loaded
      cy.get('[data-testid="idea-card"]').should('have.length.greaterThan', initialCount);
    });
  });
});

describe('Idea Detail Page', () => {
  it('displays idea details when clicking on an idea card', () => {
    // Visit the ideas page
    cy.visit('/ideas');
    
    // Wait for ideas to load
    cy.get('[data-testid="idea-card"]').should('have.length.at.least', 1);
    
    // Click on the first idea
    cy.get('[data-testid="idea-card"]').first().click();
    
    // Verify navigation to detail page
    cy.url().should('include', '/ideas/');
    
    // Check if detail components are displayed
    cy.contains('Investment Thesis').should('be.visible');
    cy.contains('Catalysts').should('exist');
    cy.contains('Performance').should('exist');
  });
});

describe('Navigation', () => {
  it('navigates between main pages', () => {
    // Start at home page
    cy.visit('/');
    
    // Go to ideas page
    cy.contains('Ideas').click();
    cy.url().should('include', '/ideas');
    
    // Go to companies page
    cy.contains('Companies').click();
    cy.url().should('include', '/companies');
    
    // Go to users page
    cy.contains('Users').click();
    cy.url().should('include', '/users');
    
    // Go back to home
    cy.contains('Home').click();
    cy.url().should('not.include', '/ideas');
  });
});