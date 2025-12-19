// Real-time payment approval system
function approvePayment(paymentId) {
    if (confirm('Are you sure you want to approve this payment?')) {
        fetch(`/admin/approve-payment/${paymentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the row without page refresh
                location.reload(); // Simple reload for now
                alert('✅ Payment approved successfully!');
            } else {
                alert('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('❌ Network error occurred');
        });
    }
}

function rejectPayment(paymentId) {
    if (confirm('Are you sure you want to reject this payment?')) {
        fetch(`/admin/reject-payment/${paymentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
                alert('❌ Payment rejected');
            } else {
                alert('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('❌ Network error occurred');
        });
    }
}

// Auto-refresh pending payments every 30 seconds
setInterval(function() {
    if (window.location.href.includes('paymenttransaction')) {
        const pendingRows = document.querySelectorAll('tr:has([style*="background: #ffc107"])');
        if (pendingRows.length > 0) {
            // Only refresh if there are pending payments
            location.reload();
        }
    }
}, 30000);

// Add pulse animation for pending payments
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
    `;
    document.head.appendChild(style);
});