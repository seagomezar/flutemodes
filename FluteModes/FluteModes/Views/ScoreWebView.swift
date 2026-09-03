import SwiftUI
import WebKit

public struct ScoreWebView: UIViewRepresentable {
    public let abcString: String

    public init(abcString: String) {
        self.abcString = abcString
    }

    public func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        let webView = WKWebView(frame: .zero, configuration: config)
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.scrollView.backgroundColor = .clear
        webView.scrollView.isScrollEnabled = true
        webView.navigationDelegate = context.coordinator

        if let templateURL = Bundle.main.url(forResource: "score_template", withExtension: "html"),
           let htmlContent = try? String(contentsOf: templateURL, encoding: .utf8) {
            webView.loadHTMLString(htmlContent, baseURL: Bundle.main.bundleURL)
        }
        return webView
    }

    public func updateUIView(_ uiView: WKWebView, context: Context) {
        context.coordinator.currentAbc = abcString
        context.coordinator.renderIfReady(uiView)
    }

    public func makeCoordinator() -> Coordinator {
        Coordinator(currentAbc: abcString)
    }

    public class Coordinator: NSObject, WKNavigationDelegate {
        var isLoaded = false
        var currentAbc: String

        init(currentAbc: String) {
            self.currentAbc = currentAbc
        }

        public func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            isLoaded = true
            renderIfReady(webView)
        }

        func renderIfReady(_ webView: WKWebView) {
            guard isLoaded else { return }
            if let json = try? JSONEncoder().encode(currentAbc),
               let jsonString = String(data: json, encoding: .utf8) {
                let js = "window.lastAbc = \(jsonString); renderScore(\(jsonString));"
                webView.evaluateJavaScript(js) { _, error in
                    if let err = error {
                        print("JavaScript renderScore error: \(err)")
                    }
                }
            }
        }
    }
}
