/* =================================================
   CartManager — localStorage-based cart system
   ================================================= */

const CartManager = {
    STORAGE_KEY: 'rangrez_cart',

    getItems() {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY)) || [];
        } catch {
            return [];
        }
    },

    saveItems(items) {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(items));
        this.updateBadge();
    },

    addItem(item) {
        const items = this.getItems();
        const existingIndex = items.findIndex(
            i => i.product_id == item.product_id && i.size === item.size
        );

        if (existingIndex > -1) {
            items[existingIndex].quantity += item.quantity;
        } else {
            items.push({
                product_id: item.product_id,
                name: item.name,
                price: parseFloat(item.price),
                image: item.image,
                slug: item.slug,
                size: item.size || '',
                quantity: item.quantity || 1,
                is_meesho_product: item.is_meesho_product || false,
                meesho_url: item.meesho_url || ''
            });
        }

        this.saveItems(items);
    },

    removeItem(productId, size) {
        let items = this.getItems();
        items = items.filter(
            i => !(i.product_id == productId && i.size === size)
        );
        this.saveItems(items);
    },

    updateQuantity(productId, size, delta) {
        const items = this.getItems();
        const item = items.find(
            i => i.product_id == productId && i.size === size
        );
        if (item) {
            item.quantity += delta;
            if (item.quantity < 1) item.quantity = 1;
            if (item.quantity > 10) item.quantity = 10;
        }
        this.saveItems(items);
    },

    getTotal() {
        return this.getItems().reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },

    getItemCount() {
        return this.getItems().reduce((sum, item) => sum + item.quantity, 0);
    },

    clearCart() {
        localStorage.removeItem(this.STORAGE_KEY);
        this.updateBadge();
    },

    updateBadge() {
        const badge = document.getElementById('cart-count-badge');
        if (badge) {
            const count = this.getItemCount();
            if (count > 0) {
                badge.textContent = count;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }
    }
};

// Initialize badge on page load
document.addEventListener('DOMContentLoaded', () => {
    CartManager.updateBadge();
});
