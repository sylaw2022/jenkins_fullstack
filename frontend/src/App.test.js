import React from 'react';
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock axios before importing App
const mockGet = jest.fn();
const mockPost = jest.fn();

jest.mock('axios', () => ({
  __esModule: true,
  default: {
    get: (...args) => mockGet(...args),
    post: (...args) => mockPost(...args)
  }
}));

import App from './App';

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  test('renders GROKLORD Fullstack Application title', () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    render(<App />);
    const titleElement = screen.getByText(/GROKLORD Fullstack Application/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders deployment information', () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    render(<App />);
    const deploymentText = screen.getByText(/Deployed with Jenkins CI\/CD & Render.com/i);
    expect(deploymentText).toBeInTheDocument();
  });

  test('displays API Health Status section', () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    render(<App />);
    const healthSection = screen.getByText(/API Health Status/i);
    expect(healthSection).toBeInTheDocument();
  });

  test('displays Backend Message section', () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    render(<App />);
    const messageSection = screen.getByText(/Backend Message/i);
    expect(messageSection).toBeInTheDocument();
  });

  test('displays Send Data to Backend form', () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    render(<App />);
    const formSection = screen.getByText(/Send Data to Backend/i);
    expect(formSection).toBeInTheDocument();
    
    const nameInput = screen.getByLabelText(/Name:/i);
    const messageInput = screen.getByLabelText(/Message:/i);
    const submitButton = screen.getByRole('button', { name: /Submit/i });
    
    expect(nameInput).toBeInTheDocument();
    expect(messageInput).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();
  });

  test('displays health status when API responds', async () => {
    const healthData = {
      status: 'ok',
      message: 'Backend API is running',
      timestamp: new Date().toISOString()
    };
    
    mockGet.mockResolvedValueOnce({ data: healthData });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    await act(async () => {
      render(<App />);
    });
    
    await waitFor(() => {
      expect(screen.getByText(/Backend API is running/i)).toBeInTheDocument();
    }, { timeout: 3000 });
    
    // Check for status indicator (✅ ok)
    const statusText = screen.getByText(/✅/i);
    expect(statusText).toBeInTheDocument();
  });

  test('displays backend message when API responds', async () => {
    const messageData = {
      message: 'Hello from the backend API!',
      environment: 'test'
    };
    
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: messageData });
    
    await act(async () => {
      render(<App />);
    });
    
    await waitFor(() => {
      expect(screen.getByText(/Hello from the backend API!/i)).toBeInTheDocument();
    });
  });

  test('allows user to input name and message', () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    
    render(<App />);
    
    const nameInput = screen.getByLabelText(/Name:/i);
    const messageInput = screen.getByLabelText(/Message:/i);
    
    fireEvent.change(nameInput, { target: { value: 'Test User' } });
    fireEvent.change(messageInput, { target: { value: 'Test Message' } });
    
    expect(nameInput.value).toBe('Test User');
    expect(messageInput.value).toBe('Test Message');
  });

  test('submits form data to backend', async () => {
    const submitResponse = {
      success: true,
      received: {
        name: 'Test User',
        message: 'Test Message',
        timestamp: new Date().toISOString()
      }
    };
    
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    mockPost.mockResolvedValueOnce({ data: submitResponse });
    
    render(<App />);
    
    const nameInput = screen.getByLabelText(/Name:/i);
    const messageInput = screen.getByLabelText(/Message:/i);
    const submitButton = screen.getByRole('button', { name: /Submit/i });
    
    fireEvent.change(nameInput, { target: { value: 'Test User' } });
    fireEvent.change(messageInput, { target: { value: 'Test Message' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith(
        expect.stringContaining('/api/data'),
        { name: 'Test User', message: 'Test Message' }
      );
    });
    
    await waitFor(() => {
      expect(screen.getByText(/Success!/i)).toBeInTheDocument();
    });
  });

  test('handles form submission error', async () => {
    mockGet.mockResolvedValueOnce({ data: { status: 'ok', message: 'Backend API is running', timestamp: new Date().toISOString() } });
    mockGet.mockResolvedValueOnce({ data: { message: 'Hello from the backend API!', environment: 'test' } });
    mockPost.mockRejectedValueOnce(new Error('Network Error'));
    
    render(<App />);
    
    const nameInput = screen.getByLabelText(/Name:/i);
    const messageInput = screen.getByLabelText(/Message:/i);
    const submitButton = screen.getByRole('button', { name: /Submit/i });
    
    fireEvent.change(nameInput, { target: { value: 'Test User' } });
    fireEvent.change(messageInput, { target: { value: 'Test Message' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Error:/i)).toBeInTheDocument();
    });
  });
});
