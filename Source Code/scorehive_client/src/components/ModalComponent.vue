<template>
  <div class="modal" :class="{ 'is-active': show }">
    <div class="modal-background" @click="$emit('close')"></div>
    <div class="modal-content">
        <div class="modal-header">
       
      </div>
     
      <!-- Add your modal content here -->
      <div class="box">
        <slot></slot>
      </div>
    </div>
    <button class="modal-close is-large" @click="$emit('close')"></button>
  </div>
  
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style scoped>
.modal {
  display: none;
}

.modal.is-active {
  display: flex;
}

.modal-background {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.modal-content {
  background-color: #fff;
  margin: auto;
  max-width: 500px;
  max-height: 80vh;
  /* overflow-y: auto; */
  border-radius: 4px;
  padding: 20px;
  position: relative;
}

.modal-close {
  background: none;
  border: none;
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  width: 24px;
  height: 24px;
}

.modal-close::before,
.modal-close::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 16px;
  height: 2px;
  background-color: #333;
  transform: translate(-50%, -50%) rotate(45deg);
}

.modal-close::after {
  transform: translate(-50%, -50%) rotate(-45deg);
}
</style>
