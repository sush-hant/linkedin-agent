"use client";

import { useMemo, useState } from "react";
import { api, ImageDraft, PostDraft } from "../lib/api";

export default function HomePage() {
  const [drafts, setDrafts] = useState<PostDraft[]>([]);
  const [images, setImages] = useState<ImageDraft[]>([]);
  const [selectedDraftId, setSelectedDraftId] = useState<string>("");
  const [editorText, setEditorText] = useState("");
  const [publishedId, setPublishedId] = useState("");
  const [status, setStatus] = useState("Idle");
  const [feedback, setFeedback] = useState({ impressions: 0, comments: 0, reposts: 0, saves: 0, quality: "average", notes: "" });

  const selectedDraft = useMemo(
    () => drafts.find((d) => d.draft_id === selectedDraftId) ?? null,
    [drafts, selectedDraftId],
  );

  const selectedImage = useMemo(
    () => images.find((img) => img.draft_id === selectedDraftId) ?? null,
    [images, selectedDraftId],
  );

  async function runPipeline() {
    setStatus("Running pipeline...");
    await api.runPipeline();
    const [d, i] = await Promise.all([api.listDrafts(), api.listImages()]);
    setDrafts(d);
    setImages(i);
    if (d[0]) {
      setSelectedDraftId(d[0].draft_id);
      setEditorText(d[0].content);
    }
    setStatus("Loaded latest drafts");
  }

  async function approve() {
    if (!selectedDraft) return;
    setStatus("Approving draft...");
    const res = await api.approveDraft(selectedDraft.draft_id, editorText);
    setPublishedId(res.published_id);
    setStatus(`Approved: ${res.published_id}`);
  }

  async function submitFeedback() {
    if (!publishedId) return;
    setStatus("Recording feedback...");
    await api.recordFeedback({
      ...feedback,
      quality: feedback.quality as "poor" | "average" | "good",
      published_id: publishedId,
      recorded_at: new Date().toISOString(),
    });
    setStatus("Feedback recorded");
  }

  return (
    <main>
      <h1>LinkedIn Agent Review UI</h1>
      <p className="small">Phase 4/5 UI: run pipeline, review/edit draft, approve, record feedback.</p>
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <button className="primary" onClick={runPipeline}>Run pipeline + load drafts</button>
        <span className="small">{status}</span>
      </div>

      <div className="grid">
        <section className="card">
          <h3>Drafts</h3>
          {drafts.length === 0 && <p className="small">No drafts yet.</p>}
          {drafts.map((d) => (
            <button
              key={d.draft_id}
              onClick={() => {
                setSelectedDraftId(d.draft_id);
                setEditorText(d.content);
              }}
              style={{ width: "100%", textAlign: "left", marginBottom: 8 }}
            >
              <div><strong>{d.style}</strong></div>
              <div className="small">{d.draft_id}</div>
            </button>
          ))}
        </section>

        <section className="card">
          <h3>Editor</h3>
          {!selectedDraft && <p className="small">Select a draft from left.</p>}
          {selectedDraft && (
            <>
              <div className="small">Topic: {selectedDraft.topic_id}</div>
              <textarea value={editorText} onChange={(e) => setEditorText(e.target.value)} />
              <div style={{ marginTop: 8 }}>
                {selectedDraft.hashtags.map((h) => <span key={h} className="pill">{h}</span>)}
              </div>
              <div style={{ marginTop: 8, display: "flex", gap: 8 }}>
                <button className="primary" onClick={approve}>Approve draft</button>
                {publishedId && <span className="small">Published ID: {publishedId}</span>}
              </div>

              <hr style={{ borderColor: "#243352", margin: "16px 0" }} />
              <h4>Image preview metadata</h4>
              {selectedImage ? (
                <>
                  <p className="small">Prompt: {selectedImage.prompt}</p>
                  <p className="small">Path: {selectedImage.file_path}</p>
                </>
              ) : <p className="small">No image for this draft.</p>}

              <hr style={{ borderColor: "#243352", margin: "16px 0" }} />
              <h4>Feedback</h4>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                <input type="number" placeholder="Impressions" value={feedback.impressions}
                       onChange={(e) => setFeedback({ ...feedback, impressions: Number(e.target.value) })} />
                <input type="number" placeholder="Comments" value={feedback.comments}
                       onChange={(e) => setFeedback({ ...feedback, comments: Number(e.target.value) })} />
                <input type="number" placeholder="Reposts" value={feedback.reposts}
                       onChange={(e) => setFeedback({ ...feedback, reposts: Number(e.target.value) })} />
                <input type="number" placeholder="Saves" value={feedback.saves}
                       onChange={(e) => setFeedback({ ...feedback, saves: Number(e.target.value) })} />
              </div>
              <div style={{ marginTop: 8 }}>
                <select value={feedback.quality}
                        onChange={(e) => setFeedback({ ...feedback, quality: e.target.value })}>
                  <option value="poor">poor</option>
                  <option value="average">average</option>
                  <option value="good">good</option>
                </select>
              </div>
              <div style={{ marginTop: 8 }}>
                <input placeholder="Notes" value={feedback.notes}
                       onChange={(e) => setFeedback({ ...feedback, notes: e.target.value })} />
              </div>
              <div style={{ marginTop: 8 }}>
                <button onClick={submitFeedback} disabled={!publishedId}>Record feedback</button>
              </div>
            </>
          )}
        </section>
      </div>
    </main>
  );
}
