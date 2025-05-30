const CACHE_NAME = 'translation-app-v2';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json'
];

// インストール時にキャッシュを作成
self.addEventListener('install', function(event) {
  console.log('Service Worker: Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Service Worker: Caching files');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('Service Worker: Cache complete');
        return self.skipWaiting();
      })
  );
});

// リクエスト時にキャッシュから返す
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // キャッシュにある場合はそれを返す
        if (response) {
          console.log('Service Worker: Serving from cache:', event.request.url);
          return response;
        }
        
        // キャッシュにない場合はネットワークから取得
        console.log('Service Worker: Fetching from network:', event.request.url);
        return fetch(event.request).then(
          function(response) {
            // 有効なレスポンスかチェック
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // レスポンスをクローンしてキャッシュに保存
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        ).catch(() => {
          // ネットワークエラー時の処理
          console.log('Service Worker: Network failed, serving offline page');
          return caches.match('/');
        });
      }
    )
  );
});

// 古いキャッシュの削除
self.addEventListener('activate', function(event) {
  console.log('Service Worker: Activating...');
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker: Claiming clients');
      return
return self.clients.claim();
   })
 );
});

// PWAインストールプロンプト用
self.addEventListener('message', function(event) {
 if (event.data && event.data.type === 'SKIP_WAITING') {
   self.skipWaiting();
 }
});
