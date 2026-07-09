import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createInteraction, updateInteraction, setCurrentInteraction } from '../store/interactionSlice';

function LogInteractionForm() {
  const dispatch = useDispatch();
  const { currentInteraction } = useSelector(state => state.interactions);
  
  const [formData, setFormData] = useState({
    hcp_id: '',
    hcp_name: '',
    interaction_type: 'in_person',
    date: new Date().toISOString().split('T')[0],
    duration_minutes: 15,
    notes: '',
    products_discussed: [],
    follow_up_required: false,
    follow_up_date: '',
  });

  const [productInput, setProductInput] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleAddProduct = () => {
    if (productInput.trim()) {
      setFormData(prev => ({ ...prev, products_discussed: [...prev.products_discussed, productInput.trim()] }));
      setProductInput('');
    }
  };

  const handleRemoveProduct = (index) => {
    setFormData(prev => ({ ...prev, products_discussed: prev.products_discussed.filter((_, i) => i !== index) }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (currentInteraction) {
        await dispatch(updateInteraction({ id: currentInteraction.id, data: formData })).unwrap();
      } else {
        await dispatch(createInteraction(formData)).unwrap();
      }
      setFormData({
        hcp_id: '', hcp_name: '', interaction_type: 'in_person',
        date: new Date().toISOString().split('T')[0], duration_minutes: 15,
        notes: '', products_discussed: [], follow_up_required: false, follow_up_date: '',
      });
      dispatch(setCurrentInteraction(null));
    } catch (error) {
      console.error('Error saving interaction:', error);
    }
  };

  return (
    <form className="interaction-form" onSubmit={handleSubmit}>
      <h2>{currentInteraction ? 'Edit Interaction' : 'Log New Interaction'}</h2>
      
      <div className="form-group">
        <label>HCP ID</label>
        <input type="text" name="hcp_id" value={formData.hcp_id} onChange={handleChange} required placeholder="e.g., HCP-2026-001" />
      </div>

      <div className="form-group">
        <label>HCP Name</label>
        <input type="text" name="hcp_name" value={formData.hcp_name} onChange={handleChange} required placeholder="Dr. John Smith" />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Interaction Type</label>
          <select name="interaction_type" value={formData.interaction_type} onChange={handleChange}>
            <option value="in_person">In-Person Visit</option>
            <option value="phone_call">Phone Call</option>
            <option value="video_call">Video Call</option>
            <option value="email">Email</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label>Date</label>
          <input type="date" name="date" value={formData.date} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Duration (minutes)</label>
          <input type="number" name="duration_minutes" value={formData.duration_minutes} onChange={handleChange} min="1" max="120" />
        </div>
      </div>

      <div className="form-group">
        <label>Notes</label>
        <textarea name="notes" value={formData.notes} onChange={handleChange} required rows="6" placeholder="Detailed notes about the interaction..." />
      </div>

      <div className="form-group">
        <label>Products Discussed</label>
        <div className="product-input">
          <input type="text" value={productInput} onChange={(e) => setProductInput(e.target.value)} placeholder="Add product name" onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddProduct())} />
          <button type="button" onClick={handleAddProduct}>Add</button>
        </div>
        <div className="product-tags">
          {formData.products_discussed.map((product, index) => (
            <span key={index} className="tag">{product}<button type="button" onClick={() => handleRemoveProduct(index)}>×</button></span>
          ))}
        </div>
      </div>

      <div className="form-row">
        <div className="form-group checkbox-group">
          <label>
            <input type="checkbox" name="follow_up_required" checked={formData.follow_up_required} onChange={handleChange} />
            Follow-up Required
          </label>
        </div>
        {formData.follow_up_required && (
          <div className="form-group">
            <label>Follow-up Date</label>
            <input type="date" name="follow_up_date" value={formData.follow_up_date} onChange={handleChange} />
          </div>
        )}
      </div>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary">{currentInteraction ? 'Update Interaction' : 'Log Interaction'}</button>
        {currentInteraction && (<button type="button" className="btn btn-secondary" onClick={() => dispatch(setCurrentInteraction(null))}>Cancel</button>)}
      </div>
    </form>
  );
}

export default LogInteractionForm;
