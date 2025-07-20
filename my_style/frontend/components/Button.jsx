import React from 'react';
import './Button.css';

const Button = ({ children, onClick, variant = 'primary', disabled = false }) => {
  const buttonClass = `button ${variant} ${disabled ? 'disabled' : ''}`;
  return (
    <button className={buttonClass} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
};

export default Button;