package com.seagomezar.flutemodes.ui

import android.annotation.SuppressLint
import android.graphics.Color
import android.view.ViewGroup
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import org.json.JSONObject

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun ScoreWebView(
    abcString: String,
    modifier: Modifier = Modifier
) {
    var webViewRef by remember { mutableStateOf<WebView?>(null) }
    var isLoaded by remember { mutableStateOf(false) }

    fun render(webView: WebView, abc: String) {
        val escaped = JSONObject.quote(abc)
        val js = "window.lastAbc = $escaped; if (typeof renderScore === 'function') { renderScore($escaped); }"
        webView.evaluateJavascript(js, null)
    }

    LaunchedEffect(abcString, isLoaded) {
        val webView = webViewRef
        if (isLoaded && webView != null) {
            render(webView, abcString)
        }
    }

    Box(modifier = modifier.fillMaxSize().background(androidx.compose.ui.graphics.Color.White)) {
        AndroidView(
            factory = { context ->
                WebView(context).apply {
                    layoutParams = ViewGroup.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                    setBackgroundColor(Color.WHITE)
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        loadWithOverviewMode = true
                        useWideViewPort = true
                        cacheMode = WebSettings.LOAD_DEFAULT
                    }
                    webViewClient = object : WebViewClient() {
                        override fun onPageFinished(view: WebView?, url: String?) {
                            super.onPageFinished(view, url)
                            isLoaded = true
                            view?.let { render(it, abcString) }
                        }
                    }
                    loadUrl("file:///android_asset/score_template.html")
                    webViewRef = this
                }
            },
            update = { webView ->
                webViewRef = webView
                if (isLoaded) {
                    render(webView, abcString)
                }
            },
            modifier = Modifier.fillMaxSize()
        )
    }
}
