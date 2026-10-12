import SwiftUI
import WebKit

public struct ScoreWebView: UIViewRepresentable {
    public let abcString: String
    public var highlightedNoteIndex: Int?

    public init(abcString: String, highlightedNoteIndex: Int? = nil) {
        self.abcString = abcString
        self.highlightedNoteIndex = highlightedNoteIndex
    }

    public func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        let webView = WKWebView(frame: .zero, configuration: config)
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.scrollView.backgroundColor = .clear
        webView.scrollView.isScrollEnabled = true
        webView.navigationDelegate = context.coordinator

        if let templateURL = Bundle.main.url(forResource: "score_template", withExtension: "html") {
            webView.loadFileURL(templateURL, allowingReadAccessTo: templateURL.deletingLastPathComponent())
        }
        return webView
    }

    public func updateUIView(_ uiView: WKWebView, context: Context) {
        context.coordinator.currentAbc = abcString
        context.coordinator.renderIfReady(uiView)
        context.coordinator.updateHighlight(uiView, noteIndex: highlightedNoteIndex)
    }

    public func makeCoordinator() -> Coordinator {
        Coordinator(currentAbc: abcString)
    }

    public class Coordinator: NSObject, WKNavigationDelegate {
        var isLoaded = false
        var currentAbc: String
        var lastRenderedAbc: String? = nil
        var lastHighlightedIndex: Int? = nil

        init(currentAbc: String) {
            self.currentAbc = currentAbc
        }

        public func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            isLoaded = true
            lastRenderedAbc = nil
            renderIfReady(webView)
        }

        public func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
            isLoaded = false
            lastRenderedAbc = nil
            if let templateURL = Bundle.main.url(forResource: "score_template", withExtension: "html") {
                webView.loadFileURL(templateURL, allowingReadAccessTo: templateURL.deletingLastPathComponent())
            }
        }

        func renderIfReady(_ webView: WKWebView) {
            guard isLoaded else { return }
            guard lastRenderedAbc != currentAbc else { return }
            lastRenderedAbc = currentAbc
            lastHighlightedIndex = nil
            if let json = try? JSONEncoder().encode(currentAbc),
               let jsonString = String(data: json, encoding: .utf8) {
                let js = """
                window.lastAbc = \(jsonString);
                if (typeof renderScore === 'function') {
                    renderScore(\(jsonString));
                }
                """
                webView.evaluateJavaScript(js, completionHandler: nil)
            }
        }

        func updateHighlight(_ webView: WKWebView, noteIndex: Int?) {
            guard isLoaded else { return }
            guard lastHighlightedIndex != noteIndex else { return }
            lastHighlightedIndex = noteIndex
            let js = (noteIndex != nil) ? "highlightNote(\(noteIndex!));" : "clearHighlight();"
            webView.evaluateJavaScript(js, completionHandler: nil)
        }
    }
}
