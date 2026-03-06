import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import BookingForm from '../code/BookingForm';

describe('BookingForm', () => {
  test('renders form fields', () => {
    render(<BookingForm listingId="listing_1" />);
    expect(screen.getByLabelText(/Start date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/End date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Guests/i)).toBeInTheDocument();
    expect(screen.getByText(/Guest information/i)).toBeInTheDocument();
  });

  test('validates required fields', async () => {
    render(<BookingForm listingId="listing_1" />);
    fireEvent.click(screen.getByText(/Book now/i));
    expect(await screen.findByText(/Start date is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/End date is required/i)).toBeInTheDocument();
  });

  test('submits successfully with valid data', async () => {
    const onSuccess = jest.fn();
    render(<BookingForm listingId="listing_1" onSubmitSuccess={onSuccess} />);

    const startInput = screen.getByLabelText(/Start date/i) as HTMLInputElement;
    const endInput = screen.getByLabelText(/End date/i) as HTMLInputElement;
    const guestInput = screen.getByLabelText(/Guests/i) as HTMLInputElement;

    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);

    startInput.value = today.toISOString().slice(0, 10);
    fireEvent.change(startInput);
    endInput.value = tomorrow.toISOString().slice(0, 10);
    fireEvent.change(endInput);
    fireEvent.change(guestInput, { target: { value: '2' } });

    fireEvent.click(screen.getByText(/Book now/i));

    await waitFor(() => expect(onSuccess).toHaveBeenCalledWith('booking_123'));
  });
});
