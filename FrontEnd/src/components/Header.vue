<template lang="">
    <div className='headerApp'>
      <nav>
        <ul>
          <RouterLink to="/" active-class="nav-active">
            <li>Películas</li>
          </RouterLink>
          <RouterLink to="/userlist" active-class="nav-active">
            <li>Valorados</li>
          </RouterLink>
          <RouterLink to="/config" active-class="nav-active">
            <li> 
              Confing
            </li>
          </RouterLink>
        </ul>
      </nav>
      <h1>¿Qué Ver Hoy?</h1>
    </div>
</template>
<script>

</script>