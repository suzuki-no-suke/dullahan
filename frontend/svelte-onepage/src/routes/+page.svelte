<script>
    import { onMount } from 'svelte';
    import SvelteMarkdown from 'svelte-markdown';
    import { Menu, MessageCircle } from 'lucide-svelte';
  
    let markdown = '# Hello, world!';
    let sidebarOpen = false;
    let mounted = false;
  
    onMount(() => {
      mounted = true;
    });
  </script>
  
  <div class="flex flex-col h-screen">
    <!-- Top bar -->
    <header class="flex items-center justify-between p-4 bg-background border-b">
      <button class="p-2 rounded-md hover:bg-gray-100" on:click={() => sidebarOpen = !sidebarOpen}>
        <Menu class="h-6 w-6" />
      </button>
      <input class="max-w-sm px-3 py-2 border rounded-md" placeholder="Untitled Document" />
      <button class="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">Save</button>
    </header>
  
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-64 bg-background border-r p-4 overflow-y-auto transition-all duration-300 ease-in-out {sidebarOpen ? 'translate-x-0' : '-translate-x-full'} absolute md:relative md:translate-x-0 h-full">
        <h2 class="text-lg font-semibold mb-4">Documents</h2>
        <ul class="space-y-2">
          <li><button class="w-full text-left px-4 py-2 rounded-md hover:bg-gray-100">Document 1</button></li>
          <li><button class="w-full text-left px-4 py-2 rounded-md hover:bg-gray-100">Document 2</button></li>
          <li><button class="w-full text-left px-4 py-2 rounded-md hover:bg-gray-100">Document 3</button></li>
        </ul>
      </aside>
  
      <!-- Main content                 -->
      <main class="flex-1 overflow-y-auto p-4">
        {#if mounted}
          <div class="h-full">
            <textarea
              bind:value={markdown}
              class="w-full h-1/2 p-2 border rounded-md mb-4"
              placeholder="Write your markdown here..."
            ></textarea>
            <div class="h-1/2 overflow-y-auto border rounded-md p-4">
              <SvelteMarkdown source={markdown} />
            </div>
          </div>
        {/if}
      </main>
    </div>
  
    <!-- Chatbot button -->
    <button
      class="fixed left-4 bottom-4 rounded-full w-12 h-12 shadow-lg bg-primary text-primary-foreground flex items-center justify-center hover:bg-primary/90"
    >
      <MessageCircle class="h-6 w-6" />
    </button>
  </div>
  
  <style>

  </style>