import React from 'react';
import LogInteractionForm from './LogInteractionForm';

function EditInteractionModal({ onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <LogInteractionForm />
      </div>
    </div>
  );
}

export default EditInteractionModal;
