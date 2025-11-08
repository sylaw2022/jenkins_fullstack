import React from 'react'
import App from '../../src/App'

describe('App Component', () => {
  beforeEach(() => {
    // Mock API responses
    cy.intercept('GET', 'http://localhost:5000/api/health', {
      statusCode: 200,
      body: {
        status: 'ok',
        message: 'Backend API is running',
        timestamp: new Date().toISOString()
      }
    }).as('healthCheck')

    cy.intercept('GET', 'http://localhost:5000/api/message', {
      statusCode: 200,
      body: {
        message: 'Hello from the backend API!',
        environment: 'test'
      }
    }).as('getMessage')

    cy.intercept('POST', 'http://localhost:5000/api/data', {
      statusCode: 200,
      body: {
        success: true,
        received: {
          name: 'Test User',
          message: 'Test Message',
          timestamp: new Date().toISOString()
        }
      }
    }).as('submitData')
  })

  it('should render the main header', () => {
    cy.mount(<App />)
    cy.contains('Jenkins Fullstack Application').should('be.visible')
  })

  it('should display API health status', () => {
    cy.mount(<App />)
    cy.wait('@healthCheck')
    cy.contains('API Health Status').should('be.visible')
  })

  it('should display backend message', () => {
    cy.mount(<App />)
    cy.wait('@getMessage')
    cy.contains('Hello from the backend API!').should('be.visible')
  })

  it('should submit form data', () => {
    cy.mount(<App />)
    
    cy.get('input[id="name"]').type('Test User')
    cy.get('textarea[id="message"]').type('Test Message')
    cy.get('button[type="submit"]').click()

    cy.wait('@submitData')
    cy.contains('Success').should('be.visible')
  })
})

