<script>
    const data = [
        {
            name: "sample",
            disp_name: "sample bot yade",
            description: "test test test",
        },
        {
            name: "sample",
            disp_name: "sample bot 2 yade",
            description: "test test test",
        }
    ];
</script>

<!-- topmenu -->
<nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a href="/">
          <img src="/dullahan.png" width="32px" height="32px" alt="アイコン & トップへ戻る" />
          <p class="large">DuLLahan</p>
      </a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start">
          <a class="navbar-item" href="/">
              Home
          </a>
          <a class="navbar-item" href="/history">
              History
          </a>
      </div>
    </div>
    <div class="navbar-end">
      <div class="navbar-item">
          <img src="/gear.svg" width="32px" height="32px" alt="設定" />
      </div>
    </div>
</nav>

<!-- left menu -->
<aside class="menu">
    <p class="menu-label">
        Items
    </p>
    <ul class="menu-list">
        <li><a href="/">Home</a></li>
        <li><a href="/history">History</a></li>
    </ul>
</aside>

<!-- 本体部分 -->
<h1>Select bots</h1>
<div class="grid">
{#each data as item}
    <div class="cell">
    <div class="card">
        <header class="card-header">
            <p class="card-holder-title">{item.disp_name}</p>
        </header>
        <div class="card-content">{item.description}</div>
        <footer class="card-footer">
            <a href="/chat/{item.name}">チャット開始する</a>
        </footer>
    </div>
    </div>
{/each}
</div>
