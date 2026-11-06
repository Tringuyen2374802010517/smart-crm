
import { apiRequest } from './client.js';

export function getTickets() {
  return apiRequest('/tickets');
}

export function getTicketById(ticketId) {
  return apiRequest(`/tickets/${encodeURIComponent(ticketId)}`);
}

export function getEligibleTechnicians(ticketId) {
  return apiRequest(
    `/assignments/eligible-technicians/${encodeURIComponent(ticketId)}`
  );
}

export function assignTechnician(ticketId, technicianId) {
  return apiRequest('/assignments/', {
    method: 'POST',
    body: JSON.stringify({
      ticket_id: Number(ticketId),
      technician_id: Number(technicianId),
    }),
  });
}


export function reassignTechnician(ticketId, technicianId, reason) {
  return apiRequest(
    `/assignments/ticket/${encodeURIComponent(ticketId)}/reassign`,
    {
      method: 'PUT',
      body: JSON.stringify({
        technician_id: Number(technicianId),
        reason: String(reason).trim(),
      }),
    }
  );
}


export function getReassignmentCandidates(ticketId) {
  return apiRequest(
    `/assignments/ticket/${encodeURIComponent(ticketId)}/reassignment-candidates`
  );
}
