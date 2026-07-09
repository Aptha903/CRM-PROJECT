import React from 'react';
import { useDispatch } from 'react-redux';
import { setCurrentInteraction, deleteInteraction, fetchInteractions } from '../store/interactionSlice';
import api from '../services/api';

function InteractionList({ interactions }) {
  const dispatch = useDispatch();

  const handleEdit = (interaction) => {
    dispatch(setCurrentInteraction(interaction));
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this interaction?')) {
      await dispatch(deleteInteraction(id)).unwrap();
      dispatch(fetchInteractions());
    }
  };

const handleComplianceCheck = async (id) => {
    try {
        const response = await api.checkCompliance(id);
        console.log('Compliance result:', response.data);
        
        // The actual data is in response.data.data (because backend returns ToolResponse)
        const complianceData = response.data.data || response.data;
        
        alert(`Compliance Check Results:\n${JSON.stringify(complianceData, null, 2)}`);
    } catch (error) {
        console.error('Compliance check error:', error);
        const errorMsg = error.response?.data?.detail || error.message || 'Unknown error';
        alert(`Compliance check failed:\n${errorMsg}`);
    }
};

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="interaction-list">
      {interactions.length === 0 ? (
        <p className="no-interactions">No interactions logged yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>HCP Name</th>
              <th>Type</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {interactions.map((interaction) => (
              <tr key={interaction.id}>
                <td>{formatDate(interaction.date)}</td>
                <td>{interaction.hcp_name}</td>
                <td>{interaction.interaction_type.replace('_', ' ').toUpperCase()}</td>
                <td>{interaction.duration_minutes} min</td>
                <td>
                  <span className={`status-badge status-${interaction.status}`}>
                    {interaction.status}
                  </span>
                </td>
                <td className="actions">
                  <button className="btn btn-small" onClick={() => handleEdit(interaction)}>Edit</button>
                  <button className="btn btn-small btn-warning" onClick={() => handleComplianceCheck(interaction.id)}>Check</button>
                  <button className="btn btn-small btn-danger" onClick={() => handleDelete(interaction.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default InteractionList;